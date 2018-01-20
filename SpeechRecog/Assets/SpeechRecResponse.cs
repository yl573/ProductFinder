using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System;

[Serializable]
public class SpeechRecResponse {
	public string RecognitionStatus;
	public string DisplayText;
	public int Offset;
	public int Duration;
}
