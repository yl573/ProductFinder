using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class TargetFoundEventHandlerTest : MonoBehaviour
{
    public VuforiaTargetManager Manager;
	// Use this for initialization
	void Start ()
	{
	    Manager.TargetFound += OnTargetFound;
	}

    private void OnTargetFound(object sender, VuforiaTargetFoundEventArgs args)
    {
        Debug.Log(args.TargetTransform);
    }

    void OnDestroy()
    {
        Manager.TargetFound -= OnTargetFound;
    }
}
