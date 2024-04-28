import Link from "next/link";
import React from "react";


export default function OrderCard(
	{
		order
	}: {
		order: any
	}
) {


	return (

		<>
			<Link href={`/dashboard/profile/order/${order?.id}`}>
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
							</div>
						</div>

					</div>
				</div>
			</Link>
		</>
	)
}