from flask import request, url_for
from sqlalchemy_filters import apply_filters


def paginate(model, schema, args_dict=None):
    page = int(request.args.get('page', 1))

    per_page = int(request.args.get('per_page', 3))
    query = model.query
    # if args_dict:
    #     page_obj = query.filter_by(**args_dict).paginate(page=page, per_page=per_page)
    # else:
    #     page_obj = query.paginate(page=page, per_page=per_page)
    if args_dict:
        page_obj = apply_filters(query, args_dict).paginate(page=page, per_page=per_page)
    else:
        page_obj = query.paginate(page=page, per_page=per_page)

    next = url_for(
        request.endpoint,
        page=page_obj.next_num if page_obj.has_next else page_obj.page,
        per_page=per_page,
        **request.view_args
    )

    prev = url_for(
        request.endpoint,
        page=page_obj.prev_num if page_obj.has_prev else page_obj.page,
        per_page=per_page,
        **request.view_args
    )
    return {'total': page_obj.total,
            'pages': page_obj.pages,
            'next': next,
            'prev': prev,
            'results': schema.dump(page_obj.items)}
