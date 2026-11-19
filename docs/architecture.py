"""Generate the README diagrams. Run from docs/: python architecture.py (needs graphviz)."""
from graphviz import Digraph

FONT = "Helvetica"


def card(title, icon, color, rows, fg="white"):
    """HTML-table card: coloured header with icon, one row per item (port = key)."""
    head = (
        f'<tr><td bgcolor="{color}" cellpadding="6" fixedsize="true" width="38" height="38">'
        f'<img src="icons/{icon}.png" scale="true"/></td>'
        f'<td bgcolor="{color}" align="left" cellpadding="6">'
        f'<font color="{fg}" point-size="14"><b>{title}</b></font></td></tr>'
    )
    body = "".join(
        f'<tr><td colspan="2" port="{port}" align="left" balign="left" cellpadding="7" bgcolor="white">'
        f'<font point-size="12"><b>{name}</b></font><br/>'
        f'<font point-size="9" color="#6E7781">{sub}</font></td></tr>'
        for port, name, sub in rows
    )
    return (
        f'<<table border="1" color="#D0D7DE" cellborder="0" cellspacing="0" style="rounded">'
        f"{head}{body}</table>>"
    )


def pill(title, icon):
    return (
        f'<<table border="1" color="#D0D7DE" cellborder="0" cellspacing="0" cellpadding="6" style="rounded" bgcolor="white"><tr>'
        f'<td fixedsize="true" width="22" height="22"><img src="icons/{icon}.png" scale="true"/></td>'
        f'<td><font point-size="12"><b>{title}</b></font></td></tr></table>>'
    )


def graph(name, direction):
    g = Digraph(name, filename=name, format="png")
    g.attr(rankdir=direction, splines="spline", nodesep="0.5", ranksep="1.0",
           bgcolor="white", pad="0.3", dpi="160", fontname=FONT)
    g.attr("node", shape="plaintext", fontname=FONT)
    g.attr("edge", fontname=FONT, fontsize="10", color="#57606A", fontcolor="#57606A", arrowsize="0.7")
    return g


# 1. What the collection does
g = graph("architecture", "LR")
g.node("ctl", card("Controller", "ansible", "#24292F", [
    ("kc", "kubectl", "delegated tasks"),
    ("pb", "ansible-playbook", "your inventory, serial: 1"),
]))
g.node("col", card("iacker.fleet", "ansible", "#CC0000", [
    ("k3s", "k3s_rolling_reboot", "preflight · cordon · reboot · Ready · uncordon"),
    ("apt", "apt_upgrade", "async dist-upgrade, survives a VPN restart"),
    ("pod", "podman_compose_update", "disk guard · backup · pull · recreate · health"),
]))
g.node("api", pill("Kubernetes API", "kubernetes"))
g.node("nodes", card("k3s nodes", "k3s", "#326CE5", [
    ("w", "workers", "one at a time"),
    ("cp", "control-plane", "last"),
])) 
g.node("podhost", card("Podman host", "podman", "#892CA0", [
    ("stack", "compose stack", "systemd unit or podman-compose"),
    ("bak", "backups", "compose, .env, data files"),
]))
g.node("ubu", pill("Ubuntu / Debian", "ubuntu"))

g.edge("ctl:pb:e", "col:apt:w")
g.edge("ctl:pb:e", "col:k3s:w")
g.edge("ctl:pb:e", "col:pod:w")
g.edge("ctl:kc:e", "api", label="cordon, Ready wait", style="dashed")
g.edge("col:apt:e", "ubu", label="SSH over VPN")
g.edge("col:k3s:e", "nodes:w:w", label="reboot")
g.edge("api:s", "nodes:n", style="dashed", arrowhead="none", label=" watch")
g.edge("col:pod:e", "podhost:stack:w", label="pull, recreate")
g.edge("col:pod:e", "podhost:bak:w", label="snapshot")
with g.subgraph() as s:
    s.attr(rank="same")
    s.node("api"); s.node("nodes"); s.node("ubu"); s.node("podhost")
    s.edge("api", "nodes", style="invis")
g.render(cleanup=True)

# 2. How a release reaches Galaxy
r = graph("release", "LR")
r.attr(ranksep="0.6")
r.node("push", pill("git push", "github"))
r.node("ci", card("GitHub Actions", "github", "#2088FF", [
    ("lint", "ansible-lint", "production profile"),
    ("san", "ansible-test sanity", "ansible-core 2.18 to 2.21"),
    ("it", "integration", "real apt + podman stack, run twice"),
]))
r.node("tag", pill("tag vX.Y.Z", "github"))
r.node("gal", pill("Ansible Galaxy", "ansible"))
r.edge("push", "ci")
r.edge("ci", "tag", label="green")
r.edge("tag", "gal", label="publish")
r.render(cleanup=True)
