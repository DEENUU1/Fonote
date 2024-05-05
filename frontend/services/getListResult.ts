export default async function getListResult(access_token: string, inputDataId: string) {
	const res = await fetch(process.env.API_URL + "ai/result/" + inputDataId, {
		method: "get",
		headers: {
			Authorization: `Bearer ${access_token}`
		}
	})
	const data = await res.json()
	console.log(data);
	console.log(res);
	return data;
}