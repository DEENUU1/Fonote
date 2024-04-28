export default async function getPlans() {
	const res = await fetch(process.env.API_URL + "subscription/plan/", {
		method: "get",
	})
	return await res.json();
}

