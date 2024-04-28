import {Chip} from "@nextui-org/react";


export default function TranscriptionColumn(
	{
		detailInputData
	}:
	{
		detailInputData: any
	}
){


	return (
		<>
			<div
				className="p-4 w-1/2 border-2 flex-grow border-gray-200 border-solid rounded-lg dark:border-gray-700 overflow-y-auto"
				style={{maxHeight: "850px"}}>
				{detailInputData?.fragments.length > 0 && (
					detailInputData?.fragments.map((detail: any) => (
						<li key={detail?.id} className={"mb-5 list-none"}>
							<div>
								<Chip color={"default"} variant={"bordered"}>
									<strong>
										{detail?.start_time?.hours}:{detail?.start_time?.minutes}:{detail?.start_time?.seconds}
									</strong>
									-
									<strong>
										{detail?.end_time?.hours}:{detail?.end_time?.minutes}:{detail?.end_time?.seconds}
									</strong>
								</Chip>
								<p>{detail?.text}</p>
							</div>
						</li>
					))
				)}
			</div>
		</>
	)
}