import React, {useEffect, useState} from "react";
import {useSession} from "next-auth/react";
import {Spinner} from "@chakra-ui/react";
import Layout from "@/components/global/Layout";
import Link from "next/link";
import {toast} from "react-toastify";
import {Button} from "@nextui-org/react";
import {subscribe} from "node:diagnostics_channel";


async function getUserSubscription(access_token: string) {
	const res = await fetch(process.env.API_URL + "subscription/subscription/", {
		method: "GET",
		headers: {
			"Authorization": `Bearer ${access_token}`
		}
	})
	return await res.json();
}


export default function UserSubscription() {

	const {data: session, status} = useSession({required: true});
	const [userSubscription, setUserSubscription] = useState(null);
	const [isLoading, setIsLoading] = useState(false);

	useEffect(() => {
		async function fetchData() {
			const res = await getUserSubscription(session?.access_token);
			setUserSubscription(res);
			console.log(res);
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

			if (res.ok){
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
						<div className="my-6 mx-auto max-w-xl">
							<h1 className="text-3xl font-extrabold text-center">Subscription</h1>
						</div>


						<div className="w-full max-w-7xl px-4 md:px-5 lg-6 mx-auto">

							<div className="w-full px-3 min-[400px]:px-6">
								<div className="flex flex-col lg:flex-row items-center py-6 border-b border-gray-200 gap-6 w-full">
									<div className="flex flex-row items-center w-full ">
										<div className="grid grid-cols-1 lg:grid-cols-2 w-full">
											<div className="flex items-center">
												<div className="">
													<h2 className="font-semibold text-xl leading-8 text-black mb-3">
														{userSubscription?.plan?.name}</h2>
													<p className="font-normal text-lg leading-8 text-gray-500 mb-3 ">
														{userSubscription?.status}
													</p>
												</div>

											</div>
											<div className="grid grid-cols-5">
												<div className="col-span-5 lg:col-span-1 flex items-center max-lg:mt-3">
													<div className="flex gap-3 lg:block">
														<p className="font-medium text-sm leading-7 text-black">Price</p>
														<p
															className="lg:mt-4 font-medium text-sm leading-7 text-indigo-600">${userSubscription?.plan?.price?.price}</p>
													</div>
												</div>
												<div className="col-span-5 lg:col-span-2 flex items-center max-lg:mt-3 ">
													<div className="flex gap-3 lg:block">
														<p className="font-medium text-sm leading-7 text-black">Start date
														</p>
														<p
															className="font-medium text-sm leading-6 whitespace-nowrap py-0.5 px-3 rounded-full lg:mt-3 bg-emerald-50 text-emerald-600">
															{userSubscription?.start_date}
														</p>
													</div>
												</div>
												<div className="col-span-5 lg:col-span-2 flex items-center max-lg:mt-3 ">
													<div className="flex gap-3 lg:block">
														<p className="font-medium text-sm leading-7 text-black">End date
														</p>
														<p
															className="font-medium text-sm leading-6 whitespace-nowrap py-0.5 px-3 rounded-full lg:mt-3 bg-red-50 text-red-600">
															{userSubscription?.end_date}
														</p>
													</div>
												</div>
											</div>
										</div>
									</div>
								</div>


							</div>
							<div
								className="w-full border-t border-gray-200 px-6 flex flex-col lg:flex-row items-center justify-between ">
								<div className="flex flex-col gap-2 sm:flex-row items-center max-lg:border-b border-gray-200">
									<Button
										onClick={(e) => handleCancelSubscription()}
										className="flex outline-0 py-6 sm:pr-6  sm:border-r border-gray-200 whitespace-nowrap gap-2 items-center justify-center font-semibold group text-lg text-black bg-white transition-all duration-500 hover:text-indigo-600">
										<svg className="stroke-black transition-all duration-500 group-hover:stroke-indigo-600"
												 xmlns="http://www.w3.org/2000/svg" width="22" height="22" viewBox="0 0 22 22"
												 fill="none">
											<path d="M5.5 5.5L16.5 16.5M16.5 5.5L5.5 16.5" stroke="" stroke-width="1.6"
														stroke-linecap="round"/>
										</svg>
										Cancel Order
									</Button>
									<Link
										href={`/dashboard/profile/order/${userSubscription?.order}`}
										className="flex outline-0 py-6 sm:pr-6  sm:border-r border-gray-200 whitespace-nowrap gap-2 items-center justify-center font-semibold group text-lg text-black bg-white transition-all duration-500 hover:text-indigo-600">
										<svg
											width="22"
											height="22"
											className="mx-auto"
											viewBox="0 0 24 24"
											fill="none"
											xmlns="http://www.w3.org/2000/svg"
										>
											<g id="SVGRepo_bgCarrier" stroke-width="0"></g>
											<g
												id="SVGRepo_tracerCarrier"
												stroke-linecap="round"
												stroke-linejoin="round"
											></g>
											<g id="SVGRepo_iconCarrier">
												{" "}
												<path
													d="M5.36328 12.0523C4.01081 11.5711 3.33457 11.3304 3.13309 10.9655C2.95849 10.6492 2.95032 10.2673 3.11124 9.94388C3.29694 9.57063 3.96228 9.30132 5.29295 8.76272L17.8356 3.68594C19.1461 3.15547 19.8014 2.89024 20.2154 3.02623C20.5747 3.14427 20.8565 3.42608 20.9746 3.7854C21.1106 4.19937 20.8453 4.85465 20.3149 6.16521L15.2381 18.7078C14.6995 20.0385 14.4302 20.7039 14.0569 20.8896C13.7335 21.0505 13.3516 21.0423 13.0353 20.8677C12.6704 20.6662 12.4297 19.99 11.9485 18.6375L10.4751 14.4967C10.3815 14.2336 10.3347 14.102 10.2582 13.9922C10.1905 13.8948 10.106 13.8103 10.0086 13.7426C9.89876 13.6661 9.76719 13.6193 9.50407 13.5257L5.36328 12.0523Z"
													stroke="#000000"
													stroke-width="2"
													stroke-linecap="round"
													stroke-linejoin="round"
												></path>
												{" "}
											</g>
										</svg>
										Order details
									</Link>
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