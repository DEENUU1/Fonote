

export default async function getInputDataDetails(access_token: string, inputDataId: string){
	const res = await fetch(process.env.API_URL + "ai/input/" + inputDataId, {
		method: "get",
		headers: {
			Authorization: `Bearer ${access_token}`
		}
	})
	return await res.json()
}