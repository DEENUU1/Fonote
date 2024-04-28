export default async function getListInputData(access_token: string) {
	const res = await fetch(process.env.API_URL + "ai/input/all/", {
		method: "get",
		headers: {
			Authorization: `Bearer ${access_token}`
		}
	})
	return await res.json()
}
