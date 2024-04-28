

export default async function getOrderList(access_token: string) {
	const res = await fetch(process.env.API_URL + "subscription/order", {
		method: "get",
		headers: {
			"Authorization": `Bearer ${access_token}`
		}
	})
	return await res.json();
}