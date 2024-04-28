
export default async function getUserSubscription(access_token: string) {
	const res = await fetch(process.env.API_URL + "subscription/subscription/", {
		method: "GET",
		headers: {
			"Authorization": `Bearer ${access_token}`
		}
	})
	return await res.json();
}
