using System;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public static class Utility
{
    public static void InvokeEvent<TEventArgs>(EventHandler<TEventArgs> eventToInvoke,
        object sender, TEventArgs args)
        where TEventArgs : EventArgs
    {
        EventHandler<TEventArgs> handler = eventToInvoke;
        if (handler != null)
        {
            handler(sender, args);
        }
    }
}
