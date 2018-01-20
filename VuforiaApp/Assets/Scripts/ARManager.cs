using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using Vuforia;

public class ARManager : MonoBehaviour {

	public GameObject ARKit;
	public Transform VuforiaOrigin;
	public VuforiaTargetManager Manager;

	void Start ()
	{
		Manager.TargetFound += OnTargetFound;
		Manager.TurnOn ();
		ARKit.SetActive (false);
	}
		
	void OnTargetFound(object sender, VuforiaTargetFoundEventArgs args) {
		ARKit.SetActive (true);
		Manager.TurnOff();
//		VuforiaOrigin.position = args.TargetTransform.position;
//		VuforiaOrigin.rotation = args.TargetTransform.rotation;
		Debug.Log ("switching");
	}

	void OnDestroy()
	{
		Manager.TargetFound -= OnTargetFound;
	}
}
