import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig } from 'vite';
import fs from 'fs';
import path from 'path';

import { viteStaticCopy } from 'vite-plugin-static-copy';

export default defineConfig({
	plugins: [
		sveltekit(),
		viteStaticCopy({
			targets: [
				{
					src: 'node_modules/onnxruntime-web/dist/*.jsep.*',

					dest: 'wasm'
				}
			]
		})
	],
	server: {
		...(process.env.NODE_ENV === 'development' && fs.existsSync(path.resolve(__dirname, 'certs/key.pem')) ? {
			https: {
				key: fs.readFileSync(path.resolve(__dirname, 'certs/key.pem')),
				cert: fs.readFileSync(path.resolve(__dirname, 'certs/cert.pem'))
			}
		} : {}),
		host: true,
		proxy: {
			// Proxy Socket.IO/WebSocket traffic to backend
			'/ws': {
				target: 'http://localhost:8080',
				changeOrigin: true,
				ws: true,
				secure: false
			}
		}
	},
	define: {
		APP_VERSION: JSON.stringify(process.env.npm_package_version),
		APP_BUILD_HASH: JSON.stringify(process.env.APP_BUILD_HASH || 'dev-build')
	},
	build: {
		sourcemap: true
	},
	worker: {
		format: 'es'
	},
	esbuild: {
		pure: process.env.ENV === 'dev' ? [] : ['console.log', 'console.debug', 'console.error']
	}
});
