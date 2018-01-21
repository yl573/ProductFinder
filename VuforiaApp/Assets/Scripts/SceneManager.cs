using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.SceneManagement;

public static class SceneManager {


	public static List<Vector2> path; 
	public static float height;

	public static void loadAR() {
		Application.LoadLevel("Main");
	}

}
