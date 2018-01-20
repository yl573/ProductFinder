using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System.Net;
using System.IO;
using System;

public class AudioRec : MonoBehaviour {
	public string RequestText;

	AudioClip myAudioClip;
	private bool _newRecording = false;
	private bool _recordingFinished = false;
	AudioSource _audioSource;

	// Use this for initialization
	void Start () {
		
	}
	
	// Update is called once per frame
	void Update () {
		if (_newRecording && !Microphone.IsRecording(null) && !_recordingFinished) {
			_newRecording = false;
			_recordingFinished = true;
			_audioSource.clip = myAudioClip;
			Debug.Log ("Stop");
			SavWav.Save (Application.dataPath+"/TempWav/testWav", _audioSource.clip);

			// First step: Send a request to the service
			HttpWebRequest request = null;
			string requestUri = "https://speech.platform.bing.com/speech/recognition/interactive/cognitiveservices/v1?language=en-GB&format=simple";
			request = (HttpWebRequest)HttpWebRequest.Create(requestUri);
			request.SendChunked = true;
			request.Accept = @"application/json;text/xml";
			request.Method = "POST";
			request.ProtocolVersion = HttpVersion.Version11;
			request.ContentType = @"audio/wav; codec=audio/pcm; samplerate=16000";
			using (StreamReader reader = new StreamReader(Application.dataPath+"/API-key.txt")){
				request.Headers["Ocp-Apim-Subscription-Key"] = reader.ReadToEnd();
			}

			// Send an audio file by 1024 byte chunks
			using (FileStream fs = new FileStream(Application.dataPath+"/TempWav/testWav.wav", FileMode.Open, FileAccess.Read))
			{

				/*
    * Open a request stream and write 1024 byte chunks in the stream one at a time.
    */
				byte[] buff = null;
				int bytesRead = 0;
				using (Stream requestStream = request.GetRequestStream())
				{
					/*
        * Read 1024 raw bytes from the input audio file.
        */
					buff = new Byte[checked((uint)Math.Min(1024, (int)fs.Length))];
					while ((bytesRead = fs.Read(buff, 0, buff.Length)) != 0)
					{
						requestStream.Write(buff, 0, bytesRead);
					}

					// Flush
					requestStream.Flush();
				}
			}
			Debug.Log ("Request sent!");

			// Second step: Process the speech recognition response
			// Get the response from the service.
			//Console.WriteLine("Response:");
			Debug.Log ("Response:");
			string responseRaw;
			SpeechRecResponse resp;
			using (WebResponse response = request.GetResponse())
			{
				Debug.Log(((HttpWebResponse)response).StatusCode);
				using (StreamReader sr = new StreamReader(response.GetResponseStream()))
				{
					responseRaw = sr.ReadToEnd();
				}
				Debug.Log(responseRaw);
				resp = JsonUtility.FromJson<SpeechRecResponse>(responseRaw);
				RequestText = resp.DisplayText;
				Debug.Log (RequestText);
			}
		}
	}

	void OnGUI()
	{
		if (GUI.Button (new Rect (10, 10, 60, 50), "Recognition")) {
			_newRecording = true;
			_recordingFinished = false;
			_audioSource = GetComponent<AudioSource> ();
			Debug.Log ("Start");
			myAudioClip = Microphone.Start (null, false, 2, 16000);
		}
	}
}



