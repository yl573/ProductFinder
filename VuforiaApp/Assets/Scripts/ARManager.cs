using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using Vuforia;

public class ARManager : MonoBehaviour {

	public GameObject ARKit;
	public Transform VuforiaOrigin;
	public VuforiaTargetManager Manager;
	public Transform ARKitCamera;

	private Vector3 _lastTargetPosition;
	private Quaternion _lastTargetRotation;
	private bool _vuforiaOriginInit = false;

	void Start ()
	{
		Manager.TargetFound += OnTargetFound;
		Manager.TurnOn ();
		ARKit.SetActive (false);
	}
		
	void OnTargetFound(object sender, VuforiaTargetFoundEventArgs args) {
		ARKit.SetActive (true);
		Manager.TurnOff ();
		//VuforiaOrigin.position = args.TargetTransform.position;
		//VuforiaOrigin.rotation = args.TargetTransform.rotation;
		_lastTargetPosition = args.TargetTransform.position;
		_lastTargetRotation = args.TargetTransform.rotation;
		Debug.Log ("switching");
		Debug.LogFormat ("Target position: {0}", args.TargetTransform.position);
		Debug.LogFormat("Target angles: {0}", args.TargetTransform.eulerAngles);

	}

//	public void Update() {
//		Debug.LogFormat ("ARKit camera position: {0}", ARKitCamera.position);
//		Debug.LogFormat ("ARKit camera rotation: {0}", ARKitCamera.eulerAngles);
//	}

	IEnumerator DelayedInitVuforiaOriginWorker()
	{
		yield return new WaitForSeconds (0.5f);
		InitVuforiaOrigin ();
	}

	public void DelayedInitVuforiaOrigin()
	{
		StartCoroutine (DelayedInitVuforiaOriginWorker ());
	}

	private void InitVuforiaOrigin()
	{
		if (!_vuforiaOriginInit) {
			VuforiaOrigin.position = ARKitCamera.position + ARKitCamera.rotation * _lastTargetPosition;
			VuforiaOrigin.rotation = ARKitCamera.rotation * _lastTargetRotation;
			_vuforiaOriginInit = true;
			Debug.LogFormat ("ARKit camera position: {0}", ARKitCamera.position);
			Debug.LogFormat ("ARKit camera rotation: {0}", ARKitCamera.eulerAngles);
		}
	}

	void OnDestroy()
	{
		Manager.TargetFound -= OnTargetFound;
	}
}
