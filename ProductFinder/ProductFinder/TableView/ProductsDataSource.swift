//
//  BooksDataSource.swift
//  ProductFinder
//
//  Created by yuxuan liu on 25/01/2018.
//  Copyright © 2018 yuxuan liu. All rights reserved.
//

import Foundation
import UIKit

class ProductsDataSource: NSObject, UITableViewDataSource, UITableViewDelegate {
    
    public var products:[String] = []
    
    //MARK: - UITableViewDataSource
    
    func numberOfSections(in tableView: UITableView) -> Int {
        return 1
    }
    
    func tableView(_ tableView: UITableView, numberOfRowsInSection section: Int) -> Int {
        return products.count
    }
    
    func tableView(_ tableView: UITableView, cellForRowAt indexPath: IndexPath) -> UITableViewCell {
        let cell = tableView.dequeueReusableCell(withIdentifier: "cell")!
        
        let text = products[indexPath.row]
        cell.textLabel?.text = text
        
        return cell
    }
    
}
