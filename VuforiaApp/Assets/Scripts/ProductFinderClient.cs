using UnityEngine;
using UnityEngine.UI;
using System.Collections;
using UnityEngine.Networking;
using System.Collections.Generic;

public class ProductList {
	public string[] products;
}

[System.Serializable]
public class ProductFinderClient: MonoBehaviour {

	public string URL = "139.59.177.111";
	private InputField SearchBarInputField;
	public ProductList productList;
	public bool productsLoaded = false;

	void Start() {
		Debug.Log ("Product Finder Client started");
	}

	void Update() {

	}

	public void Setup( InputField searchBar ) {
		this.SearchBarInputField = searchBar;
	}

	public void FindProduct() {
		productsLoaded = false;
		StartCoroutine(FindProductRoutine());
	}

	IEnumerator FindProductRoutine() {
		
		WWWForm form = new WWWForm();
		form.AddField("name", this.SearchBarInputField.text );

		UnityWebRequest www = UnityWebRequest.Post(this.URL + "/findproduct", form );
		yield return www.SendWebRequest();

		if(www.isNetworkError || www.isHttpError) {
			Debug.Log(www.error);
		}

		else {
			// Show results as text
			Debug.Log(www.downloadHandler.text);

			this.productList = JsonUtility.FromJson<ProductList>(www.downloadHandler.text);

			productsLoaded = true;

		}
	}

}