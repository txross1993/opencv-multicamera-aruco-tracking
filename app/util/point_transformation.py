import logging

logger = logging.getLogger('root'+'.' + __name__)

def transformPoint(point, transformationMtx):
    logger.debug("Running homography transformation algorithm")
    transformedPoint = [0,0]
    transformedPoint[0] = point[0] * transformationMtx[0].item(0) + point[1] * transformationMtx[0].item(1) + transformationMtx[0].item(2)
    transformedPoint[1] = point[0] * transformationMtx[1].item(0) + point[1] * transformationMtx[1].item(1) + transformationMtx[1].item(2)
    z = point[0] * transformationMtx[2].item(0) + point[1] * transformationMtx[2].item(1) + transformationMtx[2].item(2)
    transformedPoint[0] /= z
    transformedPoint[1] /= z

    return transformedPoint