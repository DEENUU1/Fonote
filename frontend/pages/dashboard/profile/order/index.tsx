import React, {useEffect, useState} from "react";
import {useSession} from "next-auth/react";
import {Spinner} from "@chakra-ui/react";
import Layout from "@/components/global/Layout";
import getOrderList from "@/services/getOrderList";
import HeaderText from "@/components/global/HeaderText";
import OrderList from "@/components/dashboard/profile/order/OrderList";


export default function Order() {

	const {data: session, status} = useSession({required: true});
	const [orderList, setOrderList] = useState<any>([]);

	useEffect(() => {
		async function fetchData() {
			const res = await getOrderList(session?.access_token);
			setOrderList(res);
		}

		fetchData();
	}, [session?.access_token]);


	if (status == "loading") {
		return <Spinner size="lg"/>;
	}

	if (session) {
		return (
			<Layout>
				<main>{
					<>
						<HeaderText text={"Order history"}/>
						<OrderList orderList={orderList}/>
					</>
				}</main>
			</Layout>
		);
	}

	return <></>;
}