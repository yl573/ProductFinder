using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class showSearchPanel : MonoBehaviour {

	public ScrollRect SearchScrollList;
	public Button ButtonComponent;


	// Use this for initialization
	void Start () {
		ButtonComponent.onClick.AddListener (HandleClick);
	}


	public void HandleClick () {
//		 set SearchScrollList to active
//		SearchScrollList.GetComponent<ScrollRect> ().enabled = true;
		ButtonComponent.enabled = false;
	}
}
