import React, {useEffect, useState} from "react";
import {useSession} from "next-auth/react";
import {Spinner} from "@chakra-ui/react";
import Layout from "@/components/global/Layout";
import {toast} from "react-toastify";
import getUserSubscription from "@/services/getUserSubscription";
import HeaderText from "@/components/global/HeaderText";
import UserSubscriptionCard from "@/components/dashboard/profile/subscription/UserSubscriptionCard";


export default function UserSubscription() {

	const {data: session, status} = useSession({required: true});
	const [userSubscription, setUserSubscription] = useState(null);
	const [isLoading, setIsLoading] = useState(false);

	useEffect(() => {
		async function fetchData() {
			const res = await getUserSubscription(session?.access_token);
			setUserSubscription(res);
		}

		fetchData()
	}, [session?.access_token]);

	const handleCancelSubscription = async () => {
		setIsLoading(true);

		try {
			const res = await fetch(process.env.API_URL + "subscription/cancel/", {
				method: "POST",
				headers: {
					"Authorization": `Bearer ${session?.access_token}`
				}
			})

			if (res.ok) {
				toast.success("Subscription cancelled")
			} else {
				toast.error("Something went wrong")
			}

		} catch (error) {
			toast.error("Something went wrong");
		} finally {
			setIsLoading(false);
		}
	}

	if (status == "loading") {
		return <Spinner size="lg"/>;
	}

	if (session) {
		return (
			<Layout>
				<main className={"h-screen"}>{
					<>
						<HeaderText text={"Subscription"}/>
						<UserSubscriptionCard
							userSubscription={userSubscription}
							handleCancelSubscription={handleCancelSubscription}
							isLoading={isLoading}
						/>
					</>
				}</main>
			</Layout>
		);
	}

	return <></>;
}