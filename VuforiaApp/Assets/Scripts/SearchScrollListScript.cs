using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

[System.Serializable]
public class Item {
	public string itemName;

}

public class SearchScrollListScript : MonoBehaviour {

	public List<Item> itemList;
	public SimpleObjectPool itemObjectPool;

	// Use this for initialization
	void Start () {
		
	}

}
