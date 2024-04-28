import {useSession} from "next-auth/react";
import Layout from "@/components/global/Layout";
import React, {useEffect, useState} from "react";
import {toast} from "react-toastify";
import getPlans from "@/services/getPlans";
import HeaderText from "@/components/global/HeaderText";
import PlanList from "@/components/subscription/PlanList";


export default function Home() {
	const {data: session, status} = useSession({required: false});
	const [plans, setPlans] = useState([]);

	useEffect(() => {
		async function fetchData() {
			const data = await getPlans();
			setPlans(data);
		}

		fetchData();
	}, []);


	const handleSubscription = async (planId: string) => {
		if (!session) {
			toast.error("Please login to continue")
			return;
		}

		try {
			const response = await fetch('http://localhost:8000/api/subscription/checkout/', {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json',
					'Authorization': `Bearer ${session?.access_token}`
				},
				body: JSON.stringify({
					plan_id: planId
				})
			});
			const res = await response.json();

			if (response.ok) {
				window.location.href = res;
			} else {
				toast.warning(res.detail)
			}
		} catch (error) {
			toast.error("Error");
		}
	};

	return (
		<>
			<Layout>
				<main>
					{
						<>
							<HeaderText text={"Plans"}/>
							<PlanList plans={plans} handleSubscription={handleSubscription}/>
						</>
					}
				</main>
			</Layout>
		</>
	);
}