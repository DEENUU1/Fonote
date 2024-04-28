import React, {useEffect, useState} from "react";
import {useSession} from "next-auth/react";
import {Spinner} from "@chakra-ui/react";
import Layout from "@/components/global/Layout";
import {useRouter} from 'next/router'
import {toast} from "react-toastify";
import getOrderDetails from "@/services/getOrderDetails";
import HeaderText from "@/components/global/HeaderText";
import {BottomOrderCardDetails, UpperOrderCardDetails} from "@/components/dashboard/profile/order/OrderCardDetails";

export default function OrderDetails() {
	const router = useRouter()
	const {data: session, status} = useSession({required: true});
	const [order, setOrder] = useState<any>(null);
	const [isLoading, setIsLoading] = useState(false);

	const handleGetInvoice = async (orderId: str) => {
		setIsLoading(true);

		try {
			const response = await fetch(process.env.API_URL + "subscription/invoice/" + orderId + "/", {
				method: "GET",
				headers: {
					accept: "application/json",
					Authorization: `Bearer ${session?.access_token}`
				}
			})

			const responseData = await response.json();

			if (responseData && responseData?.message) {
				window.location.href = responseData?.message;
			} else {
				toast.error("Something went wrong");
			}

		} catch (error) {
			toast.error("Something went wrong");
		} finally {
			setIsLoading(false);
		}

	}

	useEffect(() => {
		async function fetchData() {
			const res = await getOrderDetails(session?.access_token, router?.query?.orderId);
			setOrder(res);
			console.log(res);
		}

		fetchData();
	}, [session?.access_token, router.query.orderId]);

	if (status == "loading") {
		return <Spinner size="lg"/>;
	}

	if (session) {
		return (
			<Layout>
				<main className={"h-screen"}>{
					<>
						<HeaderText text={`Order ${router?.query?.orderId}`}/>
						<UpperOrderCardDetails order={order} isLoading={isLoading} handleGetInvoice={handleGetInvoice}
																	 router={router}/>
						<BottomOrderCardDetails order={order}/>
					</>
				}</main>
			</Layout>
		);
	}

	return <></>;
}