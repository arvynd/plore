import * as vscode from 'vscode';
import * as cp from 'child_process';
import * as path from 'path';

export function activate(context: vscode.ExtensionContext) {
	const channel = vscode.window.createOutputChannel('Plore');

	const disposable = vscode.commands.registerCommand('plore.helloWorld', () => {
		const filePath = path.join(context.extensionPath, 'samples', 'test.csv');
		runSidecar(filePath, channel);
	});

	context.subscriptions.push(disposable);
}

function runSidecar(filePath: string, channel: vscode.OutputChannel) {
	const sidecarPath = path.join(__dirname, '..', 'sidecar', 'sidecar.py');
	const proc = cp.spawn('/home/aravind/Projects/plore/.venv/bin/python', [sidecarPath, filePath]);

	const chunks: Buffer[] = [];

	proc.stdout.on('data', (chunk: Buffer) => {
		chunks.push(chunk);
	});

	proc.stdout.on('close', () => {
		const total = Buffer.concat(chunks);
		channel.appendLine(`Received ${total.length} bytes from sidecar`);
		channel.show();
	});

	proc.stderr.on('data', (data: Buffer) => {
		channel.appendLine(`[sidecar error] ${data.toString()}`);
		channel.show();
	});
}

export function deactivate() {}
