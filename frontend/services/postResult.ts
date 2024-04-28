export default async function postResponse(access_token: string, inputDataId: string, result_type: string) {
	const res = await fetch(process.env.API_URL + "ai/result/", {
		method: "post",
		headers: {
			Authorization: `Bearer ${access_token}`,
			'Content-Type': 'application/json',
			'Accept': 'application/json'
		},
		body: JSON.stringify({
			input_id: inputDataId,
			result_type: result_type
		})
	})
	return await res.json();
}
