using System.Collections;
using System.Collections.Generic;
using UnityEngine;


public class PathRenderer : MonoBehaviour {

	public GameObject WorldOrigin;

	private GameObject pathLine;

	public void Start() {
		
		RenderPath (SceneManager.path, SceneManager.height);
	}

	public void RenderPath(List<Vector2> path2d, float height) {

		Vector3[] path = ToVec3Path (path2d, height);
		pathLine = new GameObject();
		pathLine.transform.position = new Vector3 (path2d[0].x, 0, path2d[0].y);
		pathLine.AddComponent<LineRenderer>();
		LineRenderer lr = pathLine.GetComponent<LineRenderer>();
		lr.material = new Material(Shader.Find("Particles/Additive"));
		lr.SetColors(Color.red, Color.red);
		lr.SetWidth(0.05f, 0.05f);
		lr.SetVertexCount (path.Length);
		lr.SetPositions (path);
		lr.useWorldSpace = false;
		pathLine.transform.parent = WorldOrigin.transform;
	}

	private Vector3[] ToVec3Path(List<Vector2> path2d, float height) {
		Vector3[] path = new Vector3[path2d.Count];
		for (int i = 0; i < path.Length-1; i++) {
			path [i] = new Vector3 (path2d [i].x, 0, path2d [i].y);
		}
		path [path.Length-1] = new Vector3 (path2d [path.Length-1].x, height, path2d [path.Length-1].y);
		return path;
	}

	public void ClearPath() {

		GameObject.Destroy(pathLine,0);
	}

}
