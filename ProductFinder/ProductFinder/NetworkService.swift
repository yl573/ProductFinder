//
//  Network.swift
//  ProductFinder
//
//  Created by yuxuan liu on 23/01/2018.
//  Copyright © 2018 yuxuan liu. All rights reserved.
//

import Foundation

class NetworkService
{
    let defaultSession = URLSession(configuration: .default)
    var dataTask: URLSessionDataTask?
    let urlBase = "http://139.59.177.111/"
    
    func findProducts(matching searchString: String,  onResult: @escaping ([String]?) -> Void) {
        
        
        dataTask?.cancel()
        
        let postData = NSMutableData(data: ("name=" + searchString).data(using: String.Encoding.utf8)!)
        let request = NSMutableURLRequest(url: NSURL(string: urlBase + "findproduct")! as URL)
        request.httpMethod = "POST"
        request.httpBody = postData as Data
        
        dataTask = defaultSession.dataTask(with: request as URLRequest, completionHandler: { (data, response, error) -> Void in
            
            do {
                if error == nil, let data = data,
                    let json = try JSONSerialization.jsonObject(with: data) as? [String: Any],
                    let products = json["products"] as? [String]
                {
                    onResult(products)
                    print(products)
                }
                    
                else {
                    onResult(nil)
                }
            } catch {
                print("Error deserializing JSON: \(error)")
                onResult(nil)
            }
        })
        dataTask?.resume()
    }
    
    func findPath(from currentPosition: (Float,Float), to productName: String, onResult: @escaping ([(Float,Float)]?, Float?) -> Void) {
        
        dataTask?.cancel()
        
        let postData = NSMutableData(data: ("product=" + productName).data(using: String.Encoding.utf8)!)
        let positionString = "[\(currentPosition.0),\(currentPosition.1)]"
        postData.append(("&position=" + positionString).data(using: String.Encoding.utf8)!)
        
        let request = NSMutableURLRequest(url: NSURL(string: urlBase + "findpath")! as URL)
        request.httpMethod = "POST"
        request.httpBody = postData as Data
        
        dataTask = defaultSession.dataTask(with: request as URLRequest, completionHandler: { (data, response, error) -> Void in
            do {
                if error == nil, let data = data, let json = try JSONSerialization.jsonObject(with: data) as? [String: Any],
                    let height = json["height"] as? Float,
                    let rawPath = json["path"] as? [[Float]]
                {
                    var path: [(Float,Float)] = []
                    for point in rawPath {
                        path += [(point[0],point[1])]
                    }
                    onResult(path, height)
                }
                else {
                    onResult(nil,nil)
                }
            }
            catch{
                print("Error deserializing JSON: \(error)")
                onResult(nil,nil)
            }
            
        })
        dataTask?.resume()
    }
}

