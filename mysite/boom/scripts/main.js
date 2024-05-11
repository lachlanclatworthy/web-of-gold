import * as THREE from 'three';

// Setup view
const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(
	75,
	window.innerWidth / window.innerHeight,
	0.1,
	1000
);
const renderer = new THREE.WebGLRenderer(window.innerWidth, window.innerHeight);
document.body.appendChild(renderer.domElement)

// *CUBES OF MANY COLOURS*
const geometry = new THREE.BoxGeometry(3,3,3);
const cubes = [
	new THREE.Mesh(
		geometry,
		new THREE.MeshBasicMaterial({color:0x00FFFF})
	),
]

// It's weird that frame update is tied to the rotation like this
function animate() {
	requestAnimationFrame(animate);

	// Spin every which way
	cubes.forEach((c) => {
		c.rotation.x += 0.02;
		c.rotation.y += 0.02;
		c.rotation.z += 0.02;
	});

	renderer.render(scene, camera);
}

cubes.forEach((c) => {
	scene.add(c)
});

// Shift back to a reasonable position
camera.position.z = 10;

animate();
