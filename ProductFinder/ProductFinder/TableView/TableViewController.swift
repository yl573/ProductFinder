//
//  TableViewController.swift
//  ProductFinder
//
//  Created by yuxuan liu on 25/01/2018.
//  Copyright © 2018 yuxuan liu. All rights reserved.
//

import UIKit

class TableViewController: UIViewController, UITableViewDelegate {
    
    
    @IBOutlet var tableView: UITableView!
    public var searchText: String = ""
    private let dataSource = ProductsDataSource()
    private let networkService = NetworkService()
    
    override func viewDidLoad() {
        super.viewDidLoad()
        tableView.dataSource = dataSource
        
        networkService.findProducts(matching: searchText) { (products: [String]?) in
            guard let products = products else {return}
            if products.count > 0 {
                self.dataSource.products = products
                DispatchQueue.main.async{
                    self.tableView.reloadData()
                }
            }
        }
    }
    
    override func prepare(for segue: UIStoryboardSegue, sender: Any?) {
        if segue.identifier == "showAR"
        {
            if let destinationVC = segue.destination as? ViewController {
                destinationVC.product = dataSource.products[0]
            }
        }
    }
    
}
