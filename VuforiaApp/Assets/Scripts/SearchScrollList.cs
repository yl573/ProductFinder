using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

[System.Serializable]

public class SearchScrollList : MonoBehaviour {

	private ProductList productList;

	public bool isPopulated = false;
	public GameObject prefabItemButton;
	public GameObject prefabNoResultLabel;
	public Transform contentPanel;
	public ProductFinderClient pfc;

	// Use this for initialization
	void Start () {
		
	}

	void Update() {
		if (pfc.productsLoaded && isPopulated == false) {
			// is loaded
			productList = pfc.productList;
			removeAllItems ();
			UpdateScrollList ();
		}
	}

	public void UpdateScrollList() {
		isPopulated = true;
		if (productList.products.Length == 0) {
			GameObject noResultObject = (GameObject)GameObject.Instantiate (prefabNoResultLabel);
			noResultObject.transform.SetParent(contentPanel, false);
			return;
		}
		foreach ( string product in productList.products ) {
			GameObject newButtonObject = (GameObject)GameObject.Instantiate (prefabItemButton);
			newButtonObject.transform.SetParent(contentPanel, false);

			ItemButton newButtonComponent = newButtonObject.GetComponent<ItemButton>();
			newButtonComponent.Setup( product );
		}

	}

	public void removeAllItems() {
		for ( int i =  contentPanel.childCount - 1; i > 0; i --) 
		{
			GameObject toRemove = contentPanel.GetChild(i).gameObject;
			Destroy (toRemove);
		}
	}
}
