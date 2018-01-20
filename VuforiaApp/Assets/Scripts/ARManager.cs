using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using Vuforia;

public class ARManager : MonoBehaviour {

	public GameObject Vuforia;
	public GameObject ARKit;
	public Transform VuforiaOrigin;

	void Start () {
//		ARKit.SetActive (false);
//		Vuforia.SetActive (true);
		ARKit.SetActive (true);
		Vuforia.SetActive (false);
	}

	void OnTargetDetected(VuforiaTargetFoundEventArgs args) {
		ARKit.SetActive (true);
		Vuforia.SetActive (false);
		VuforiaOrigin.position = args.TargetTransform.position;
		VuforiaOrigin.rotation = args.TargetTransform.rotation;
		Debug.Log ("switching");
	}
}
