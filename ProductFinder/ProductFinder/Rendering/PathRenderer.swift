//
//  PathRenderer.swift
//  ProductFinder
//
//  Created by yuxuan liu on 25/01/2018.
//  Copyright © 2018 yuxuan liu. All rights reserved.
//

import Foundation
import SceneKit

class PathRenderer {
    
    func renderPath(for path: [(Float, Float)], height: Float, parent: SCNNode) {
        
        guard let lastPoint = path.last else {
            print("Empty path")
            return
        }
        
        var path3D = converTo3DPath(path2D: path, height: height)
        path3D.append(SCNVector3(lastPoint.0,lastPoint.1,height))
        
        for i in 0...path3D.count-2 {
            let line = Line(parent: parent, start: path3D[i], end: path3D[i+1], radius: 0.005, color: UIColor.red)
            parent.addChildNode(line)
        }
    }
    
    private func converTo3DPath(path2D: [(Float, Float)], height: Float) -> [SCNVector3]{
        
        var path3D:[SCNVector3] = []
        for point in path2D {
            path3D.append(SCNVector3(point.0,point.1,0))
        }
        print(path3D)
        
        return path3D
    }
    
//    func removePath() {
//        localOrigin.ch
//    }
}
