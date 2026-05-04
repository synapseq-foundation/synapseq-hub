export interface ParsedDescription {
	lines: string[]
}

export async function fetchSpsqFile(path: string): Promise<string> {
	const response = await fetch("/" + path)
	if (!response.ok) {
		throw new Error(`Failed to fetch spsq file: ${response.statusText}`)
	}
	return response.text()
}

export function parseDescription(content: string): ParsedDescription {
	const lines = content.split("\n")
	const descriptionLines = lines
		.filter((line) => line.startsWith("##"))
		.map((line) => {
			const withoutPrefix = line.slice(2)
			return withoutPrefix.trim()
		})

	return { lines: descriptionLines }
}

export async function getAudioDescription(path: string): Promise<string[]> {
	const content = await fetchSpsqFile(path)
	const parsed = parseDescription(content)
	return parsed.lines
}
