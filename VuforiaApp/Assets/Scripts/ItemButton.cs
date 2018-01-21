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

	private ProductFinderClient productFinderClientComponent;
	private GameObject SearchScrollListObject;
	private Button ActivationButton;


	void Start () {
		button.onClick.AddListener (HandleClick);
		productFinderClientComponent.onPathLoaded += OnPathLoaded;
	}

	void OnPathLoaded(object sender, EventArgs args) {
		
		SceneManager.path = productFinderClientComponent.productPath.path;
		SceneManager.height = productFinderClientComponent.productPath.height;
		SceneManager.loadAR ();	

//		SearchScrollListObject.SetActive (false);
//		ActivationButton.enabled = true;
	}

	public void Setup( string productName, ProductFinderClient pfc, GameObject ssl, Button ab ) {
		this.productName = productName;
		this.productFinderClientComponent = pfc;
		this.SearchScrollListObject = ssl;
		this.ActivationButton = ab;
		itemText.text = productName;
	}

	public void HandleClick () {
		// handle the click on the product
		productFinderClientComponent.FindPath(this.productName);
	}

}
