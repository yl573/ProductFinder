using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

[System.Serializable]
public class SearchButton : MonoBehaviour {

	public Button buttonComponent;
	public SearchScrollList searchScrollList;
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
		searchScrollList.isPopulated = false;
		productFinderClient.FindProduct ();

//		List<Vector2> path = new List<Vector2> ();
//		path.Add (new Vector2(0,0));
//		path.Add (new Vector2(1,0));
//		path.Add (new Vector2(1,1));
//		path.Add (new Vector2(0,1));
//		SceneManager.path = path;
//		SceneManager.height = 0;
//		SceneManager.loadAR ();
	}
}
