using UnityEngine;
using UnityEngine.UI;
using System.Collections;
using UnityEngine.Networking;
using System.Collections.Generic;
using SimpleJSON;
using System;

public class ProductList {
	public string[] products;
}

public class ProductPath {
	public List<Vector2> path;
	public float height;

}

[System.Serializable]
public class ProductFinderClient: MonoBehaviour {

	private InputField SearchBarInputField;

	public string URL = "139.59.177.111";
	public ProductList productList;
	public ProductPath productPath;
	public bool productsLoaded = false;
	public event EventHandler onPathLoaded;

	void Start() {
		this.productPath = new ProductPath ();
		this.productPath.path = new List<Vector2> ();
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

	public void FindPath(string productName) {
		StartCoroutine(FindPathRoutine(productName));
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

	IEnumerator FindPathRoutine(string productName) {

		WWWForm form = new WWWForm();
		form.AddField("product", productName );
		form.AddField("position", "(0,0)" );

		UnityWebRequest www = UnityWebRequest.Post(this.URL + "/findpath", form );
		yield return www.SendWebRequest();

		if(www.isNetworkError || www.isHttpError) {
			Debug.Log(www.error);
		}

		else {
			// Show results as text
			Debug.Log(www.downloadHandler.text);

			var N = JSON.Parse(www.downloadHandler.text);

			this.productPath.height = N ["height"];

			for (int i = 0; N ["path"] [i] != null; i++) {
				var newVect = new Vector2 (0f, 0f);

				newVect.x = N ["path"] [i] [0];
				newVect.y = N ["path"] [i] [1];

				this.productPath.path.Add (newVect);

			}

			onPathLoaded(null, EventArgs.Empty);

		}
	}

}