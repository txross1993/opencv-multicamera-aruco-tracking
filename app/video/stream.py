from threading import Thread
from .frame import AbstractFrame, NullFrame, Frame
import re
import cv2, logging
import numpy as np
from generic_base_classes.subject import AbstractSubject
from expiringdict import ExpiringDict
from util.uri_factory.stream_uri_builder import StreamUri
from util import file_loader
import re
from time import sleep
from .stream_status import StreamStatus
from util import timestamper
from util.counts_per_sec import CountsPerSec as CPS
from os import environ

logger = logging.getLogger('root'+'.' + __name__)

class VideoStream(AbstractSubject):
	

	def __init__(self, stream_id):
		super().__init__()
		# initialize the video camera stream and read the first frame
		# from the stream
		self.name = stream_id
		self.stream_id_file_pattern = r'^{}\..*$'.format(self.name)
		self._fps = 1
		self.stream = None 		
		(self.grabbed, self.frame) = (None, None)
		self._mtx=None
		self._dist=None
		self._transformationMtx=None
		self.roi=None
		self.newcameramtx=None
		self.status = StreamStatus.STOPPED
		self.stream_sleep = float(environ['STREAM_SLEEP'])
		self.read_sleep = float(environ['READ_SLEEP'])
		self.uri=self.getUri()
 
		# initialize the variable used to indicate if the thread should
		# be stopped
		self.stopped = False

		# Stream metric health
		self._metrics = ExpiringDict(max_len=1, max_age_seconds=60) # this expires after 60 seconds unless it's updated
		self._metrics.update({'framesRead': 0})

		

	def getUri(self):
		uri = StreamUri(self.name).uri
		logging.debug("Stream uri for stream ID {}: {}".format(self.name, uri))
		return uri

	@property
	def fps(self):
		return self._fps

	def setFps(self, fps):
		self._fps = fps
		self.stream.set(cv2.CAP_PROP_FPS, fps)	
		logger.debug("Set stream {} FPS to {}".format(self.name, self._fps))

	@property
	def mtx(self):
		return self._mtx

	@property
	def dist(self):
		return self._dist

	@property
	def transformationMtx(self):
		return self._transformationMtx

	def setupStream(self):
		logger.debug("Entering setup for stream {}".format(self.name))
		''' While not READY or REJECTED '''
		try:
			self.set_intrinsic_calibration()
			#self._setUndistortionParameters()
			self.set_transformation_matrix()

			if self.status!=StreamStatus.REJECTED:
				self.set_video_capture()
				if self.stream.isOpened():
					self.set_ready()
				else:
					self.set_rejected()

			if self.status != StreamStatus.REJECTED:
				self.set_ready()

			logger.debug("Sucessfully setup stream {}".format(self.name))
			
		except Exception as e:
			logger.error(e)
			self.stream = None
			self.set_rejected()

	def set_intrinsic_calibration(self):
		
		intrinsic_calibration = self._getIntrinsicCalibrationFile('data/intrinsic_calibration')
		if intrinsic_calibration is not None:	
			self._mtx=intrinsic_calibration['mtx']	
			#self._dist=intrinsic_calibration['dist']
			self._dist=0
			logger.debug("Successfully set intrinsic calibration parameters for stream: {}".format(self.name))
		else:
			self.set_rejected()

	def set_video_capture(self):
		self.stream = cv2.VideoCapture(self.uri)
		self.stream.set(cv2.CAP_PROP_FPS, self._fps)
		(self.grabbed, self.frame) = self.stream.read()
		# if self.grabbed:
		# 	cv2.imwrite('{}_stream_{}.jpg'.format(str(timestamper.getNow()),str(self.name)), self.frame)
		logging.debug("Setup stream for stream {} First frame grabbed? {} Frame data {}".format(self.name, self.grabbed, self.frame))

	def set_transformation_matrix(self):
		 
		homography = VideoStream._getCalibrationFile(self.stream_id_file_pattern, 'data/homography_calibration')
		if homography is not None:
			self._transformationMtx = homography
			logger.debug("Successfully set transformation matrix for stream: {}".format(self.name))
		else:
			self.set_rejected()
	
	def _getIntrinsicCalibrationFile(self, relativeDirectory):
		calibrationFiles = file_loader.walkDir(relativeDirectory)
		calibration=None
		if int(self.name)>6 and int(self.name)<27:
			pattern=r"M3058"
		else:
			pattern=r"Q3518"
		for filename in calibrationFiles:
			if re.search(pattern, filename):
				stream_calibration=file_loader.findRelativeFilePath(relativeDirectory +'/{}'.format(filename))
				calibration = file_loader.unpickle(stream_calibration)
		return calibration

	@staticmethod
	def _getCalibrationFile(stream_id_file_pattern, relativeDirectory):
		calibrationFiles = file_loader.walkDir(relativeDirectory)
		calibration=None
		for filename in calibrationFiles:
			if re.search(stream_id_file_pattern, filename):
				stream_calibration=file_loader.findRelativeFilePath(relativeDirectory +'/{}'.format(filename))
				calibration = file_loader.unpickle(stream_calibration)
		return calibration

	def _setUndistortionParameters(self):
		try:
			w = self.frame.shape[:2][1]
			h = self.frame.shape[:2][0]
			newcameramtx, roi = cv2.getOptimalNewCameraMatrix(self._mtx, self._dist, (w,h), 1, (w,h))
			self.newcameramtx = newcameramtx
			self.roi = roi
			logger.debug("Successfully set undistortion parameters for stream: {}".format(self.name))
		except AttributeError as e:
			logger.error(e)
			logger.error("Unable to set undistortion parameters for stream {}".format(self.name))

	def set_ready(self):
		self.status = StreamStatus.READY

	def set_rejected(self):
		self.status = StreamStatus.REJECTED

	def set_running(self):
		self.status = StreamStatus.RUNNING

	def set_stopped(self):
		self.stopped = True
		self.status = StreamStatus.STOPPED

	def start(self):
		# start the thread to read frames from the video stream
		if self.status == StreamStatus.READY:
			Thread(target=self.update, args=()).start()
			logger.info("STARTED - Stream started for id {}".format(self.name))
			self.set_running()
		else:
			self.set_rejected()
		return self

	def sendHeartbeat(self, framesRead):
		try:
			numFramesRead = self._metrics['framesRead']
			self._metrics.update({'framesRead': numFramesRead+framesRead})
		except KeyError: # catching in case the metrics have expired
			logging.ERROR("Stream heartbeat expired - it's been 60 seconds since a frame was read. Resetting metric")
			self._metrics.update({'framesRead': framesRead})
		#logger.info("STILL RUNNING - Stream {} number of frames read {}".format(self.name, self._metrics))
 
	def update(self):
		# keep looping infinitely until the thread is stopped
		framesRead = 0
		logger.debug("ENTERING - update loop for video stream {}".format(self.name))
		
		cps = CPS().start()
		while True:
			# if the thread indicator variable is set, stop the thread
			if self.stopped:
				logging.debug("Stream {} set to STOPPED".format(self.name))
				return
 
			# otherwise, read the next frame from the stream
			sleep(self.stream_sleep)			
			try:
				#previous_frame = self.frame
				self.set_video_capture()
				logging.debug("IN stream update loop, attempting to grab frames for stream {}".format(self.name))
				(self.grabbed, self.frame) = self.stream.read()
				logging.debug("Read frame from stream {}!".format(self.name))
				#logger.debug("Previous Frame is equal to next frame: {}".format(np.array_equal(previous_frame, self.frame)))
				if self.grabbed:
					framesRead+=1
				if framesRead >=8: # Once we have read 8 frames, send the heartbeat
					self.sendHeartbeat(framesRead)
					framesRead = 0
			except Exception as e:
				logger.error(e)
				self.grabbed=False
			self.stream.release()
			logger.info(
            	"Loop iterations/sec: {:.0f}".format(cps.countsPerSec()))
			cps.increment()
 
	def read(self) -> Frame:
		# return the frame most recently read
		sleep(self.read_sleep)
		
		logging.debug("Stream.read() called. Frame grabbed? {} Frame data: {}".format(self.grabbed, self.frame))
		if self.grabbed and self.frame.any():
		    frame =  Frame(self.frame, 
						 self.name,
						 mtx=self.mtx,
						 dist=self.dist,
						 transformationMtx=self.transformationMtx,
						 newcameramtx=self.newcameramtx,
						 roi=self.roi)
		else:
			frame = NullFrame()
		
		logging.debug("Stream.read() called for stream {}. Frame is of type {}".format(self.name, type(frame)))
		return frame
 
	def stop(self):
		# indicate that the thread should be stopped
		logger.debug("Stop called for stream {}".format(self.name))
		self.set_stopped()

	def set_read_sleep(self, read_sleep):
		self.read_sleep=read_sleep
		logger.debug("Set READ_SLEEP to %d" % self.read_sleep)