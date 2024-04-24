import React, {useEffect, useState} from "react";
import {useSession} from "next-auth/react";
import {Spinner} from "@chakra-ui/react";
import Layout from "@/components/Layout";
import {toast} from "react-toastify";
import {Button} from "@nextui-org/react";

async function getOrderList(access_token: string) {
	const res = await fetch(process.env.API_URL + "subscription/order", {
		method: "get",
		headers: {
			"Authorization": `Bearer ${access_token}`
		}
	})
	return await res.json();
}


export default function Order() {

	const {data: session, status} = useSession({required: true});
	const [orderList, setOrderList] = useState<any>([]);
	const [isLoading, setIsLoading] = useState(false);

	useEffect(() => {
		async function fetchData() {
			const res = await getOrderList(session?.access_token);
			setOrderList(res);
			console.log(res);
		}

		fetchData();
	}, [session?.access_token]);

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


	if (status == "loading") {
		return <Spinner size="lg"/>;
	}

	if (session) {
		return (
			<Layout>
				<main>{
					<>
						<div className="my-6 mx-auto max-w-xl">
							<h1 className="text-3xl font-extrabold text-center">Order history</h1>
						</div>

						<div className="w-full max-w-7xl px-4 md:px-5 lg-6 mx-auto">
							<div className="main-box border border-gray-200 rounded-xl pt-6 max-w-xl max-lg:mx-auto lg:max-w-full">
								<div className="w-full px-3 min-[400px]:px-6">

									{Array.isArray(orderList) && (
										orderList.map((order) => (
											<div
												key={order?.id}
												className="flex flex-col lg:flex-row items-center py-6 border-b border-gray-200 gap-6 w-full">
												<div className="flex flex-row items-center w-full ">
													<div className="grid grid-cols-1 lg:grid-cols-2 w-full">
														<div className="flex items-center">
															<div className="">
																<h2 className="font-semibold text-xl leading-8 text-black mb-3">
																	{order?.plan?.name}</h2>
															</div>

														</div>
														<div className="grid grid-cols-5">
															<div className="col-span-5 lg:col-span-1 flex items-center max-lg:mt-3">
																<div className="flex gap-3 lg:block">
																	<p className="font-medium text-sm leading-7 text-black">Price</p>
																	<p
																		className="lg:mt-4 font-medium text-sm leading-7 text-indigo-600">{order?.total_amount} {order?.currency}</p>
																</div>
															</div>
															<div className="col-span-5 lg:col-span-2 flex items-center max-lg:mt-3">
																<div className="flex gap-3 lg:block">
																	<p className="font-medium text-sm whitespace-nowrap leading-6 text-black">
																		Date</p>
																	<p
																		className="font-medium text-base whitespace-nowrap leading-7 lg:mt-3 text-emerald-500">
																		{order?.created_at}</p>
																</div>
															</div>
															<div className="col-span-5 lg:col-span-2 flex items-center max-lg:mt-3 ">
																<div className="flex gap-3 lg:block">
																	<p className="font-medium text-sm leading-7 text-black">Invoice
																	</p>
																	<Button
																		onClick={(e) => handleGetInvoice(order?.id)}
																		className="font-medium text-sm leading-6 whitespace-nowrap py-0.5 px-3 rounded-full lg:mt-3 bg-emerald-50 text-emerald-600">
																		Get invoice
																	</Button>
																</div>
															</div>

														</div>
													</div>

												</div>
											</div>
										))
									)}
								</div>
							</div>
						</div>


					</>
				}</main>
			</Layout>
		);
	}

	return <></>;
}