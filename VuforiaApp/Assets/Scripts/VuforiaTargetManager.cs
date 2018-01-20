using System;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class VuforiaTargetManager : MonoBehaviour
{
    public event EventHandler<VuforiaTargetFoundEventArgs> TargetFound;
    public GameObject VuforiaCamera;
    public Transform TrackedTarget;

    public void TurnOff()
    {
        VuforiaCamera.SetActive(false);
    }

    public void TurnOn()
    {
        VuforiaCamera.SetActive(true);
    }

    public void OnTargetFound()
    {
        VuforiaTargetFoundEventArgs args = new VuforiaTargetFoundEventArgs(TrackedTarget);
        Utility.InvokeEvent(TargetFound, this, args);
    }
}
