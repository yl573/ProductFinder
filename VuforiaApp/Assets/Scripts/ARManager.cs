using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using Vuforia;

public class ARManager : MonoBehaviour {

	public GameObject Vuforia;
	public GameObject ARKit;

	// Use this for initialization
	void Start () {
		ARKit.SetActive (false);
		Vuforia.SetActive (true);
	}

	void OnGUI() {

		if (GUI.Button (new Rect (10, 70, 50, 30), "Switch")) {
			ARKit.SetActive (true);
			Vuforia.SetActive (false);
			Debug.Log ("switching");
			// VuforiaBehaviour.Instance.enabled = false;
		}
	}

}
