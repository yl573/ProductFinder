//
//  SearchViewController.swift
//  ProductFinder
//
//  Created by yuxuan liu on 25/01/2018.
//  Copyright © 2018 yuxuan liu. All rights reserved.
//

import UIKit

class SearchViewController: UIViewController {
    
    @IBOutlet weak var textField: UITextField!
    
    override func prepare(for segue: UIStoryboardSegue, sender: Any?) {
        guard let text = textField.text else {return}
        if segue.identifier == "showTable"
        {
            if let destinationVC = segue.destination as? TableViewController {
                destinationVC.searchText = text
            }
        }
    }
    
    override func viewDidLoad() {
        super.viewDidLoad()
    }
}
