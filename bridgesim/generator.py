import io

from .trusscalc.truss import Result, init_truss, Truss, plot_diagram

def generate_bridge(width: float, height: float, elements: int, load: float) -> Truss:
    t = init_truss('bridge truss')

    width = width * 1000.0
    height = height * 1000.0

    element_width = width / elements

    bottom_joints = []  # Bottom joints of the truss
    top_joints = []     # Top joints of the truss

    # Bottom joints
    for n in range(elements + 1):
        x = n * element_width
        y = 0.0
        name = chr(65 + n)
        bottom_joints.append(dict(name=name, x=x, y=y))

    # Top joints
    for n in range(elements):
        # offset by half an element
        x = (element_width / 2.0) + (n * element_width)
        y = height
        name = chr(65 + n + len(bottom_joints))
        top_joints.append(dict(name=name, x=x, y=y))

    t.add_joints(bottom_joints + top_joints)

    print("Bottom joints:", bottom_joints)
    print("Top joints:", top_joints)

    bars = []

    for n in range(elements):
        b1 = bottom_joints[n]['name'] + bottom_joints[n+1]['name']
        b2 = bottom_joints[n]['name'] + top_joints[n]['name']
        b3 = bottom_joints[n+1]['name'] + top_joints[n]['name']
        bars.extend([b1, b2, b3])
        if n > 0:
            b4 = top_joints[n-1]['name'] + top_joints[n]['name']
            bars.append(b4)

    print("Bars:", bars)

    t.add_bars(bars)

    supports = [(bottom_joints[0]['name'], 'pin'), (bottom_joints[-1]['name'], 'roller')]

    print("Supports:", supports)

    t.add_supports(supports)

    if load:
        load = load / (len(bottom_joints) - 2)  # Spread load along the joints, except the supports
        for n in range(len(bottom_joints) - 2):
            name = f"L{n+1}"
            joint_name = bottom_joints[n+1]['name']
            joint_load = dict(name=name, joint_name=joint_name, x=0, y=load * -1.0)
            print("Load:", joint_load)
            t.add_loads([joint_load])

    return t


def generate_bridge_svg(width: float, height: float, elements: int, load: float) -> bytes:
    t = generate_bridge(width, height, elements, load)

    r = Result(t)
    print("Result:", r)

    buf = io.BytesIO()
    plot_diagram(t, r, save_to=buf, save_to_format="svg")

    v = buf.getvalue()
    return v
