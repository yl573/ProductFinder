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

    func getProducts(searchString: String) {
        
        let postData = NSMutableData(data: ("name="+searchString).data(using: String.Encoding.utf8)!)
        
        let request = NSMutableURLRequest(url: NSURL(string: "http://139.59.177.111/findproduct")! as URL)
        request.httpMethod = "POST"
        request.httpBody = postData as Data
        
        let session = URLSession.shared
        let dataTask = session.dataTask(with: request as URLRequest, completionHandler: { (data, response, error) -> Void in
            if (error != nil) {
                print(error)
            } else {
                let httpResponse = response as? HTTPURLResponse
                
                guard let data = data else {return}
                let resultNSString = NSString(data: data as Data, encoding: String.Encoding.utf8.rawValue)!
                let resultString = resultNSString as String
                
                print(resultString)
            }
        })
        
        dataTask.resume()
        
    }
}

