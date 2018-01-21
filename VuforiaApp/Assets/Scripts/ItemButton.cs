using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System;
using UnityEngine.UI;

public class ItemButton : MonoBehaviour {

	private string productName;
	private bool pathLoaded = false;

	public Button button;
	public Text itemText;
	public ProductFinderClient productFinderClientComponent;


	void Start () {
		button.onClick.AddListener (HandleClick);
		productFinderClientComponent.onPathLoaded += OnPathLoaded;
	}

	void OnPathLoaded(object sender, EventArgs args) {
		SceneManager.path = productFinderClientComponent.productPath.path;
		SceneManager.height = productFinderClientComponent.productPath.height;
		SceneManager.loadAR ();	
	}

//	void Update() {
//		if ( productFinderClientComponent.pathLoaded && this.pathLoaded != true ) {
//			this.pathLoaded = true;
//			SceneManager.path = new List<Vector2> ();
//			SceneManager.path = productFinderClientComponent.productPath.path;
//			SceneManager.height = productFinderClientComponent.productPath.height;
//			SceneManager.loadAR ();
//		}
//	}

	public void Setup( string productName, ProductFinderClient pfc ) {
		this.productName = productName;
		this.productFinderClientComponent = pfc;
		itemText.text = productName;
	}

	public void HandleClick () {
		// handle the click on the product
		productFinderClientComponent.FindPath(this.productName);
	}

}
