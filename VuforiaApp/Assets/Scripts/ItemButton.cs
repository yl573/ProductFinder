using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class ItemButton : MonoBehaviour {

	public Button button;
	public Text itemText;


	// Use this for initialization
	void Start () {
		button.onClick.AddListener (HandleClick);
	}

	public void Setup( string productName ) {
		itemText.text = productName;
	}

	public void HandleClick () {
		// handle the click on the product
	}

}
