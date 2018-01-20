using System;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class VuforiaTargetFoundEventArgs : EventArgs
{
    public Transform TargetTransform { get; set; }

    public VuforiaTargetFoundEventArgs(Transform targetTransform)
    {
        TargetTransform = targetTransform;
    }
}
