using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Point
{
	public float x, y;
	public Point(float xpos, float ypos) {
		x = xpos;
		y = ypos;
	}
}

public class PathRenderer : MonoBehaviour {

	public GameObject WorldOrigin;

	private List<GameObject> lines;

	public void Start() {
		lines = new List<GameObject> ();
		List<Point> path = new List<Point> ();
		path.Add (new Point (0, 0));
		path.Add (new Point (1, 0));
		path.Add (new Point (1, 1));
		path.Add (new Point (0, 1));
		RenderPath (path, -1);
	}

	public void RenderPath(List<Point> path, float z) {
		for (int i = 0; i < path.Count-1; i++) {
			// switch z and y
			Vector3 start = new Vector3 (path [i].x, z, path [i].y);
			Vector3 end = new Vector3 (path [i + 1].x, z, path [i + 1].y);
			GameObject line = DrawLine(start, end, Color.red);
			line.transform.parent = WorldOrigin.transform;
			lines.Add (line);
			Debug.Log ("line added: " + start + " to " + end);
		}
	}

	public void ClearPath() {
		foreach (GameObject line in lines) {
			GameObject.Destroy(line, 0);
		}
	}

	private GameObject DrawLine(Vector3 start, Vector3 end, Color color)
	{
		GameObject myLine = new GameObject();
		myLine.transform.position = start;
		myLine.AddComponent<LineRenderer>();
		LineRenderer lr = myLine.GetComponent<LineRenderer>();
		lr.material = new Material(Shader.Find("Particles/Alpha Blended Premultiply"));
		lr.SetColors(color, color);
		lr.SetWidth(0.1f, 0.1f);
		lr.SetPosition(0, start);
		lr.SetPosition(1, end);
		return myLine;
	}

}
