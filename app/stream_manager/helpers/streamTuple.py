from detection_pipeline.stream_detector_wrapper import StreamSubjectDetectorWrapper

class StreamTuple:

    def __init__(self, stream_id, stream_detector:StreamSubjectDetectorWrapper):
        self._stream_id = stream_id
        self._stream_detector = stream_detector


    def __repr__(self):
        return "({}, {})".format(self._stream_id, self._stream_detector.streamName)

    def __eq__(self, secondTuple)->bool:
        return(self.stream_id==secondTuple.stream_id)

    @property
    def stream_id(self):
        return self._stream_id

    @property
    def stream_detector(self):
        return self._stream_detector

