export default async function getOrderDetails(access_token: string, orderId: string) {
	const res = await fetch(process.env.API_URL + "subscription/order/" + orderId, {
		method: "get",
		headers: {
			"Authorization": `Bearer ${access_token}`
		}
	})
	return await res.json();
}