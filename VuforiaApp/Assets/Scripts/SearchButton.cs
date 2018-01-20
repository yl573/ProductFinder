using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class SearchButton : MonoBehaviour {

	public Button buttonComponent;
	public InputField searchBarInputField;
	public ProductFinderClient productFinderClient;

	// Use this for initialization
	void Start () {
		buttonComponent.onClick.AddListener (HandleClick);
		productFinderClient.Setup (searchBarInputField);
	}
	
	// Update is called once per frame
	void Update () {
		
	}

	public void HandleClick() {
		productFinderClient.FindProduct ();
	}
}
