import {Button} from "@chakra-ui/react";
import React from "react";


export function UpperOrderCardDetails(
	{
		order,
		isLoading,
		handleGetInvoice,
		router
	}:
	{
		order: any
		isLoading: boolean
		handleGetInvoice: any,
		router: any
	}
){

	return (
		<>
			<div className="w-full max-w-7xl px-4 md:px-5 lg-6 mx-auto">
				<div className="main-box border border-gray-200 rounded-xl pt-6 max-w-xl max-lg:mx-auto lg:max-w-full">
					<div className="w-full px-3 min-[400px]:px-6">
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
													className="lg:mt-4 font-medium text-sm leading-7 text-indigo-600">${order?.total_amount}</p>
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
													isLoading={isLoading}
													onClick={(e) => handleGetInvoice(router?.query?.orderId)}
													className="font-medium text-sm leading-6 whitespace-nowrap py-0.5 px-3 rounded-full lg:mt-3 bg-emerald-50 text-emerald-600">
													Get invoice
												</Button>
											</div>
										</div>

									</div>
								</div>

							</div>
						</div>
					</div>
				</div>
			</div>
		</>
	)
}


export function BottomOrderCardDetails(
	{
		order
	}:{
		order: any
	}
){

	return (
		<>
			<div className="w-full max-w-7xl px-4 md:px-5 lg-6 mx-auto">
				<div className="main-box border border-gray-200 rounded-xl pt-6 max-w-xl max-lg:mx-auto lg:max-w-full">
					<div className="w-full px-3 min-[400px]:px-6">
						<div className="grid grid-cols-2 gap-6">
							<div className="col-span-1">
								<p className="font-medium text-sm leading-7 text-black">City: <strong>{order?.city}</strong></p>
								<p className="font-medium text-sm leading-7 text-black">Country: <strong>{order?.country}</strong>
								</p>
							</div>
							<div className="col-span-1">
								<p className="font-medium text-sm leading-7 text-black">Email: <strong>{order?.email}</strong></p>
								<p className="font-medium text-sm leading-7 text-black">Phone: <strong>{order?.phone}</strong></p>
							</div>
							<div className="col-span-1">
								<p className="font-medium text-sm leading-7 text-black">Address
									line1: <strong>{order?.line1}</strong></p>
								<p className="font-medium text-sm leading-7 text-black">Address
									line2: <strong>{order?.line2}</strong></p>
							</div>
							<div className="col-span-1">
								<p className="font-medium text-sm leading-7 text-black">Postal
									code: <strong>{order?.postal_code}</strong>
								</p>
								<p className="font-medium text-sm leading-7 text-black">State: <strong>{order?.state}</strong></p>
							</div>
						</div>
					</div>
				</div>
			</div>
		</>
	)
}