using System;
using System.Collections.Generic;
using UnityEngine;

namespace LakeviewChinese {
    public sealed class ChineseOverlay : MonoBehaviour {
        private static bool created;
        private SpriteRenderer[] sprites = new SpriteRenderer[0];
        private Camera[] cameras = new Camera[0];
        private float nextScan;
        private bool show = true;
        private int appearanceMode;
        private Font font;
        private GUIStyle style;
        private readonly Dictionary<string, Entry[]> entries = OverlayData.Create();

        public static void Install() {
            if (created) return;
            created = true;
            GameObject root = new GameObject("Lakeview Chinese Image Overlay");
            UnityEngine.Object.DontDestroyOnLoad(root);
            root.AddComponent<ChineseOverlay>();
        }
        private void Awake() {
            appearanceMode = Mathf.Clamp(PlayerPrefs.GetInt(Appearance.PreferenceKey, Appearance.DefaultMode), 0, Appearance.PanelAlpha.Length-1);
            try { font = Font.CreateDynamicFontFromOSFont(new string[] { "Microsoft YaHei", "SimHei", "Arial Unicode MS" }, 24); }
            catch (Exception ex) { Debug.LogWarning("Chinese image overlay font: " + ex.Message); }
            Debug.Log("Lakeview Chinese image overlay loaded. F8 toggles original/Chinese; F7 cycles light/no/clear background.");
        }
        private void Update() {
            if (Input.GetKeyDown(KeyCode.F8)) show = !show;
            if (Input.GetKeyDown(KeyCode.F7)) {
                appearanceMode = (appearanceMode + 1) % Appearance.PanelAlpha.Length;
                PlayerPrefs.SetInt(Appearance.PreferenceKey, appearanceMode);
                PlayerPrefs.Save();
            }
            if (Time.realtimeSinceStartup < nextScan) return;
            nextScan = Time.realtimeSinceStartup + 0.3f;
            sprites = UnityEngine.Object.FindObjectsOfType<SpriteRenderer>();
            cameras = UnityEngine.Object.FindObjectsOfType<Camera>();
            Array.Sort(sprites, delegate(SpriteRenderer a, SpriteRenderer b) {
                if (a == null || b == null) return 0;
                return a.sortingOrder.CompareTo(b.sortingOrder);
            });
        }
        private bool ScreenRect(SpriteRenderer sr, out Rect rect) {
            rect = new Rect();
            Camera chosen = null;
            foreach (Camera cam in cameras) {
                if (cam == null || !cam.enabled || !cam.gameObject.activeInHierarchy || cam.targetTexture != null) continue;
                if ((cam.cullingMask & (1 << sr.gameObject.layer)) == 0) continue;
                if (chosen == null || cam.depth > chosen.depth) chosen = cam;
            }
            if (chosen == null) return false;
            // Tight sprite meshes omit transparent margins. Map the full source rect instead
            // so paper headlines and atlas slices use the same coordinates as the preview.
            Sprite sprite = sr.sprite;
            Vector2 pivot = sprite.pivot;
            float unit = sprite.pixelsPerUnit;
            float left = -pivot.x / unit, bottom = -pivot.y / unit;
            float right = left + sprite.rect.width / unit, top = bottom + sprite.rect.height / unit;
            float minX=float.MaxValue,minY=float.MaxValue,maxX=float.MinValue,maxY=float.MinValue;
            for (int corner=0;corner<4;corner++) {
                float x=(corner & 1)==0 ? left : right;
                float y=(corner & 2)==0 ? bottom : top;
                if (sr.flipX) x=-x;
                if (sr.flipY) y=-y;
                Vector3 point=chosen.WorldToScreenPoint(sr.transform.TransformPoint(new Vector3(x,y,0)));
                if (point.z<=0f) return false;
                minX=Mathf.Min(minX,point.x);maxX=Mathf.Max(maxX,point.x);
                minY=Mathf.Min(minY,point.y);maxY=Mathf.Max(maxY,point.y);
            }
            rect = Rect.MinMaxRect(minX, Screen.height-maxY, maxX, Screen.height-minY);
            return rect.width > 5 && rect.height > 4 && rect.xMax > 0 && rect.yMax > 0 && rect.x < Screen.width && rect.y < Screen.height;
        }
        private void OnGUI() {
            if (!show || font == null || Event.current.type != EventType.Repaint) return;
            if (style == null) {
                style = new GUIStyle(GUI.skin.label);
                style.font = font;
                style.wordWrap = true;
                style.richText = false;
                style.padding = new RectOffset(0, 0, 0, 0);
                style.margin = new RectOffset(0, 0, 0, 0);
            }
            Color oldColor = GUI.color;
            int oldDepth = GUI.depth;
            GUI.depth = -9999;
            foreach (SpriteRenderer sr in sprites) {
                if (sr == null || !sr.enabled || !sr.gameObject.activeInHierarchy || sr.sprite == null || sr.color.a < 0.04f) continue;
                Entry[] labels;
                string qualified = sr.sprite.texture.name + "|" + sr.sprite.name;
                if (!entries.TryGetValue(qualified, out labels) && !entries.TryGetValue(sr.sprite.name, out labels)) continue;
                Rect screen;
                if (!ScreenRect(sr, out screen)) continue;
                foreach (Entry label in labels) {
                    if (label.Note && screen.width < 90f) continue; // Never enlarge a tiny pickup icon into a reading panel.
                    float x=sr.flipX ? 1f-label.X-label.W : label.X;
                    float y=sr.flipY ? 1f-label.Y-label.H : label.Y;
                    Rect box = new Rect(screen.x + screen.width * x, screen.y + screen.height * y, screen.width * label.W, screen.height * label.H);
                    float panelAlpha = label.Note ? Appearance.NoteAlpha[appearanceMode] : Appearance.PanelAlpha[appearanceMode];
                    if (panelAlpha > 0f) {
                        GUI.color = new Color(0.17f, 0.17f, 0.17f, panelAlpha * sr.color.a);
                        GUI.DrawTexture(box, Texture2D.whiteTexture);
                    }
                    float padding = label.Note ? Mathf.Max(4f, box.width * 0.035f) : Mathf.Max(1f, box.height * 0.05f);
                    Rect textBox = new Rect(box.x + padding, box.y + padding, box.width - 2 * padding, box.height - 2 * padding);
                    style.alignment = label.Note ? TextAnchor.UpperLeft : TextAnchor.MiddleCenter;
                    style.fontStyle = label.Note ? FontStyle.Normal : FontStyle.Bold;
                    int desired = label.Note ? Mathf.RoundToInt(box.width / 12f) : Mathf.RoundToInt(box.height * 0.72f);
                    desired = Mathf.Clamp(desired, 9, 64);
                    GUIContent content = new GUIContent(label.Text);
                    for (style.fontSize = desired; style.fontSize > 8; style.fontSize--) {
                        if (style.CalcHeight(content, textBox.width) <= textBox.height && (label.Note || style.CalcSize(content).x <= textBox.width)) break;
                    }
                    float brightness = Mathf.Max(sr.color.r, Mathf.Max(sr.color.g, sr.color.b));
                    if (sr.sprite.name.StartsWith("PauseMenuConfirm_") && label.Y >= 0.49f && !label.Bright) brightness *= 0.42f;
                    GUI.color = Color.white;
                    // A thin glyph outline preserves contrast without covering the artwork.
                    style.normal.textColor = new Color(0f, 0f, 0f, Appearance.OutlineAlpha * sr.color.a);
                    GUI.Label(new Rect(textBox.x-1f,textBox.y,textBox.width,textBox.height), content, style);
                    GUI.Label(new Rect(textBox.x+1f,textBox.y,textBox.width,textBox.height), content, style);
                    GUI.Label(new Rect(textBox.x,textBox.y-1f,textBox.width,textBox.height), content, style);
                    GUI.Label(new Rect(textBox.x,textBox.y+1f,textBox.width,textBox.height), content, style);
                    style.normal.textColor = new Color(label.Bright ? 1f : Mathf.Max(0.4f, brightness), label.Bright ? 0.96f : Mathf.Max(0.4f, brightness), label.Bright ? 0.88f : Mathf.Max(0.4f, brightness), sr.color.a);
                    GUI.Label(textBox, content, style);
                }
            }
            GUI.color = oldColor;
            GUI.depth = oldDepth;
        }
    }
    public sealed class Entry {
        public readonly string Text;
        public readonly float X,Y,W,H;
        public readonly bool Note, Bright;
        public Entry(string text, float x, float y, float w, float h, bool note, bool bright) {
            Text=text; X=x; Y=y; W=w; H=h; Note=note; Bright=bright;
        }
    }
}
